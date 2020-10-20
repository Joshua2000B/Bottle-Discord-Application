<html>
<head>
<title>All Messages</title>
</head>
<body>
<table border="1">
%for row in rows:
    <tr>
        <td>{{str(row[0])}}</td>
        <td>{{str(row[1])}}</td>
        <td>{{str(row[2])}}</td>
    </tr>
%end
</table>
<a href="/">Back</a>
<a href="/send_message">Send a new message..."</a>
</body>
</html>
