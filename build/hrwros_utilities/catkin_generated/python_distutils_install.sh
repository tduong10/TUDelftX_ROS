#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/timmy/hrwros_ws/src/hrwros/hrwros_utilities"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/timmy/hrwros_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/timmy/hrwros_ws/install/lib/python2.7/dist-packages:/home/timmy/hrwros_ws/build/hrwros_utilities/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/timmy/hrwros_ws/build/hrwros_utilities" \
    "/usr/bin/python2" \
    "/home/timmy/hrwros_ws/src/hrwros/hrwros_utilities/setup.py" \
    build --build-base "/home/timmy/hrwros_ws/build/hrwros_utilities" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/timmy/hrwros_ws/install" --install-scripts="/home/timmy/hrwros_ws/install/bin"
