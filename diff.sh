diff -r -w -q --exclude=lib /e/ . 
diff -r -w -q --exclude=lib /e/ . | \
  grep "differ" | \
  sed 's/Files \(.*\) and \(.*\) differ/"\1" "\2"/' | \
  while read file1 file2; do
    echo code --diff $file1 $file2
  done
