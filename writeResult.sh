#!/bin/bash

dir=/var/www/html/iptv/reverse/your_playlist.m3u    //m3uplaylist
myreferer=
cek=$(sed -n '7p' ${dir})
status_code=$(curl --referer ${myreferer} --write-out %{http_code} --silent --output /dev/null ${cek})

echo "$dir" | grep -oP '(?<=reverse/)[^<]*'| sed 's/\(^\|$\)/*****/g'

#check http status
if [[ "$status_code" -ne 200 ]] || [ -z "$cek" ] ; then
  echo "Site status changed to $status_code"  
  echo -e "generate new playlist........"
  out_dir='/var/www/html/iptv/selenium'          //script and output.txt dir
  python3 $out_dir/your_code.py
  sleep 5
  source=$( sed -n '1p' $out_dir/output.txt | sed '1s/^.//')
    sleep 1
    echo "NEW URL....."
    echo -e ${source}
    old=$(sed -n '/EXT-X-STREAM-INF/{n;p;}'  ${dir})
    sleep 1
    echo "Last Url Code $status_code"
    echo -e ${old}
    sleep 2
    echo -e 'write to m3u'
    sed -i "7s|^.*$||" ${dir}
    sleep 2
    sed -i "7s|^.*|${source//&/\\&}|" ${dir}
    echo -e 'OK'  
else
   echo "Playlist Active"
   exit 0
fi
