
# Install

```
pip install bookmd
```

# Usage

```
Usage: bookmd [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  init
  query
  template
  transform
```

## `init`

initialize directory structure.

```
$ mkdir /some/directory
$ cd /some/directory
$ bookmd init
$ ls -al
total 0
drwxr-xr-x   4 haoxun  staff  136 Dec  8 21:58 .
drwxr-xr-x  24 haoxun  staff  816 Dec  8 21:56 ..
drwxr-xr-x   3 haoxun  staff  102 Dec  8 20:35 .bookmd-db
drwxr-xr-x   3 haoxun  staff  102 Dec  8 17:50 isbn
```

## `query`

drop one or more ISBN files to the `./isbn`, then run

```
$ bookmd query
```

this command would query douban api for book infos and cache the result to
`./.bookmd-db`.

## `template`

generate markdown template.


```
$ bookmd template list ./template.md
$ bookmd template list --keys='title,rating[average]' ./template.md
$ bookmd template table ./template.md
$ bookmd template table --keys='title,rating[average]' ./template.md
```

example of `list`:

```
* <!-- 算法设计与分析基础 --> {{ isbn="9787302311850" template="[{title}]({alt})" }}
* <!-- 金领简历 --> {{ isbn="9787115279262" template="[{title}]({alt})" }}
* <!-- R语言编程艺术 --> {{ isbn="9787111423140" template="[{title}]({alt})" }}
* <!-- 计算广告 --> {{ isbn="9787115392497" template="[{title}]({alt})" }}
* <!-- Word Power Made Easy --> {{ isbn="9781101873854" template="[{title}]({alt})" }}
```

example of `table`:

```
| title | author | rating |
| --- | --- | --- |
{{ isbn="9787302311850" template="| <!-- 算法设计与分析基础 -->  [{title}]({alt}) | {author[0]} | {rating[average]} |" }}
{{ isbn="9787115279262" template="| <!-- 金领简历 -->  [{title}]({alt}) | {author[0]} | {rating[average]} |" }}
{{ isbn="9787111423140" template="| <!-- R语言编程艺术 -->  [{title}]({alt}) | {author[0]} | {rating[average]} |" }}
{{ isbn="9787115392497" template="| <!-- 计算广告 -->  [{title}]({alt}) | {author[0]} | {rating[average]} |" }}
{{ isbn="9781101873854" template="| <!-- Word Power Made Easy -->  [{title}]({alt}) | {author[0]} | {rating[average]} |" }}
```

## `transform`

render templates.

```
$ bookmd transform ./template.md ./doc.md
```

example of generaeted:

```
* <!-- 算法设计与分析基础 --> [算法设计与分析基础](https://book.douban.com/subject/24708288/)
* <!-- 金领简历 --> [金领简历](https://book.douban.com/subject/10779571/)
* <!-- R语言编程艺术 --> [R语言编程艺术](https://book.douban.com/subject/24699632/)
* <!-- 计算广告 --> [计算广告](https://book.douban.com/subject/26596778/)
* <!-- Word Power Made Easy --> [Word Power Made Easy](https://book.douban.com/subject/25977798/)
```
