IFS=. read -r projectid datasetid tableid

cat <<EOF
in/param/projectid=inline:$projectid
in/param/datasetid=inline:$datasetid
in/param/tableid=inline:$tableid
EOF
