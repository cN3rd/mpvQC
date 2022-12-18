#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ctypes
import platform

import inject
from PySide6.QtCore import QSize
from PySide6.QtCore import Slot, Signal
from PySide6.QtOpenGL import QOpenGLFramebufferObject
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickFramebufferObject
from mpv import MpvRenderContext, MpvGlGetProcAddressFn

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcMpvFrameBufferObjectPyObject(QQuickFramebufferObject):
    """ Adapted from https://gitlab.com/robozman/python-mpv-qml-example """

    sig_on_update = Signal()

    def __init__(self):
        super().__init__()
        self.sig_on_update.connect(self.do_update)

    @Slot()
    def do_update(self):
        self.update()

    def createRenderer(self) -> QQuickFramebufferObject.Renderer:
        return Renderer(self)


class Renderer(QQuickFramebufferObject.Renderer):
    """"""

    def __init__(self, parent):
        super(Renderer, self).__init__()
        self._parent = parent
        self._get_proc_address_resolver = MpvGlGetProcAddressFn(GetProcAddressGetter().wrap)
        self._ctx = None

        from mpvqc.services.player import PlayerService
        self._player_service = inject.instance(PlayerService)

    def createFramebufferObject(self, size: QSize) -> QOpenGLFramebufferObject:
        if self._ctx is None:
            self._ctx = MpvRenderContext(
                self._player_service.mpv,
                api_type='opengl',
                opengl_init_params={'get_proc_address': self._get_proc_address_resolver}
            )
            self._ctx.update_cb = self._parent.sig_on_update.emit

        return QQuickFramebufferObject.Renderer.createFramebufferObject(self, size)

    def render(self):
        if self._ctx:
            factor = self._parent.scale()
            rect = self._parent.size()

            width = int(rect.width() * factor)
            height = int(rect.height() * factor)
            fbo = int(self.framebufferObject().handle())

            self._ctx.render(flip_y=False, opengl_fbo={'w': width, 'h': height, 'fbo': fbo})


class GetProcAddressGetter:
    """ fixme: Class gets obsolete once https://bugreports.qt.io/browse/PYSIDE-971 gets fixed """

    def __init__(self):
        self._func = self._find_platform_wrapper()

    def _find_platform_wrapper(self):
        os = platform.system()
        if os == 'Linux':
            return self._init_linux()
        elif os == 'Windows':
            return self._init_windows()
        raise f'Platform {os} not supported'

    def _init_linux(self):
        try:
            from OpenGL import GLX
            return self._glx_impl
        except AttributeError:
            pass
        try:
            from OpenGL import EGL
            return self._egl_impl
        except AttributeError:
            pass
        raise 'Cannot initialize OpenGL'

    def _init_windows(self):
        from PySide6.QtGui import QOpenGLContext
        import glfw

        from PySide6.QtGui import QOffscreenSurface
        self.surface = QOffscreenSurface()
        self.surface.create()

        if not glfw.init():
            raise 'Cannot initialize OpenGL'

        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(1, 1, "mpvQC-OpenGL", None, None)

        glfw.make_context_current(window)
        QOpenGLContext.currentContext().makeCurrent(self.surface)
        return self._windows_impl

    def wrap(self, _, name: bytes):
        address = self._func(name)
        return ctypes.cast(address, ctypes.c_void_p).value

    @staticmethod
    def _glx_impl(name: bytes):
        from OpenGL import GLX
        return GLX.glXGetProcAddress(name.decode("utf-8"))

    @staticmethod
    def _egl_impl(name: bytes):
        from OpenGL import EGL
        return EGL.eglGetProcAddress(name.decode("utf-8"))

    @staticmethod
    def _windows_impl(name: bytes):
        import glfw
        return glfw.get_proc_address(name.decode('utf8'))