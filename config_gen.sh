#!/bin/bash 
echo "Enter the path to 'SelectedImages' folder"
read data

jq -n "{labels: [],imageURLs: [],annotationURLs: []}" > $data/Config/example.json

for file in $data/*; do
    if [ ${file: -4} == ".jpg" ]
    then
        jq --arg imageURLs "data/images/""${file##*/}" '.imageURLs|=.+[$imageURLs]' $data/Config/example.json>$data/Config/temp.json
        cp $data/Config/temp.json $data/Config/example.json 
        filenamewithextension="${file##*/}"
        jq --arg annotationURLs "data/annotations/""${filenamewithextension%.*}"".png" '.annotationURLs|=.+[$annotationURLs]' $data/Config/example.json>$data/Config/temp.json
        cp $data/Config/temp.json $data/Config/example.json
    fi      
done

                  jq --slurpfile labels $data/Config/labels.txt '.labels=$labels' $data/Config/example.json>$data/Config/temp.json
                  cp  $data/Config/temp.json $data/Config/example.json 
                  rm $data/Config/temp.json
