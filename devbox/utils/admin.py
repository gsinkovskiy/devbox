def run_as_admin(exe, params, as_admin = True):
    from subprocess import Popen, PIPE
    import platform
    import os
    import win32com.shell.shell as shell
    import win32con
    from win32process import GetExitCodeProcess
    import win32event
    import pywintypes

    try:
        # Try to launch process as administrator in case exception was
        # due to insufficient privileges.
        # To make process call block, set `fMask` parameter to return
        # handle to process that can be monitored to wait for the
        # process to exit.  See the [SHELLEXECUTEINFO structure
        # documentation][1] for details.
        #
        # [1]: https://msdn.microsoft.com/en-us/library/windows/desktop/bb759784%28v=vs.85%29.aspx
        SEE_MASK_NOASYNC = 0x00000100
        SEE_MASK_NOCLOSEPROCESS = 0x00000040
        WAIT_FOREVER = -1

        launch_kwargs = dict(lpFile=exe, lpParameters=params,
                                nShow=win32con.SW_SHOW,
                                fMask=(SEE_MASK_NOASYNC |
                                    SEE_MASK_NOCLOSEPROCESS))
        if as_admin:
            launch_kwargs['lpVerb'] = 'runas'
        process_info = shell.ShellExecuteEx(**launch_kwargs)
        win32event.WaitForSingleObject(process_info['hProcess'],
                                        WAIT_FOREVER)
        return_code = GetExitCodeProcess(process_info['hProcess'])
        if return_code == 0:
            return ''
        else:
            raise RuntimeError('Process returned error code: %s' % return_code)

    except pywintypes.error as e:
        if e.winerror == 1223:  # Error 1223 is elevation cancelled.
            raise CancelAction(e.strerror)
        else:
            raise

def is_admin():
    import ctypes

    return ctypes.windll.shell32.IsUserAnAdmin()
