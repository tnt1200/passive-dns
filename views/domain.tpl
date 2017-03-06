<!DOCTYPE html>
<html>
<head>
    <title> passive dns collector </title>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" href="static/css/zTreeStyle/zTreeStyle.css" type="text/css">
    <script type="text/javascript" src="static/js/jquery-1.4.4.min.js"></script>
    <script type="text/javascript" src="static/js/jquery.ztree.core.js"></script>
</head>

<body>
<h1>domains</h1>
<div class="content_wrap">
<ul>
  % for item in dl:
    <li><a href="/{{item.tld_name}}">{{item.tld_name}}</li>
  % end
</ul>
</div>
</body>
</html>