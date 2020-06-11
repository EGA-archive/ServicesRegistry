

if __name__ == '__main__':
    import sys
    from .dispatcher import main

    if len(sys.argv) > 1: # Unix socket
        main(path=sys.argv[1])
    else: # host:port
        main()
