#!/usr/bin/env ruby

require 'feh/bin'

if __FILE__ == $0 then
    if ($*.length != 1) then exit(1) end
    data = Feh::Bin.decompress(IO.binread($*[0]))
    print(data)
end
