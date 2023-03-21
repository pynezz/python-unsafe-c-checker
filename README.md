# Unsafe C checker
A script that looks for unsafe C functions in your source code and avoids unneccessary lost points on the exam.

## Example usage
Just download/copy paste the script and use it with either:

```bash
chmod +x unsafe_checker.py
```

Verbose output, recursive search in current directory:
```
./unsafe_checker.py -v[erbose] -r[ecursive] . -o result.txt  
```

or:
(with verbose output, recursive search in current directory)
```bash
python3 unsafe_checker.py -v[erbose] -r[ecursive] . -o result.txt  
```


### Verbose
Gives more information, including alternative safer functions  

# Screenshots
[!alt(img)]
