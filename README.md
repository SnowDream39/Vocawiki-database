# Vocawiki 辅助信息数据库

## 这个数据库的作用是什么？

Vocawiki 从 VocaDB 导入P主歌曲列表、歌曲资料等信息。但是这些信息本身没有和 Vocawiki 相关联。这个数据库提供一些将 Vocawiki 与 VocaDB 里面的条目相关联的数据。Vocawiki 的前端在获取 VocaDB 数据的同时获取这个数据库里面的数据，然后生成条目内容。

## 这个数据库保存哪些信息？

数据库保存有以下信息：

1. VocaDB 歌曲id对应的本站条目
1. VocaDB P主id对应的本站条目
1. 从 VocaDB 歌曲自动筛选P主作品列表的结果之后，进一步提供一个增删名单

## 这个数据库不保存哪些信息？

1. VOCALOID Songbox 的颜色外观
1. P主歌曲列表中的额外说明部分
