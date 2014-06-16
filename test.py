def testmmap():
    import mmap
    # write a simple example file
    with open("Main.xml", "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        # read content via standard file methods
        line = mm.readline()
        while line:
            line = mm.readline()
            if 'name=' in line:
                print line
                line = mm.readline()
                print 'write string'
                mm.write('mystring')
                mm.flush()
   #               mm[0:2]="my"
            # read content via slice notation
#            print mm[:5]  # prints "Hello"
            # update content using slice notation;
            # note that new content must have same size
            # ... and read again using standard file methods
 #           mm.seek(0)
  #          print mm.readline()  # prints "Hello  world!"
            # close the map
        mm.close()
if __name__=='__main__':
    testmmap()
