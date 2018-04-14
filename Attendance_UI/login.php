<?php
$user = $_POST['user'];
$pass = $_POST['pass'];
if($user == "Aditya" || $user == "Abhishek" && $pass == "student") {
	header("Location:student.php?user=".$user);
}
else if($user == "Teacher" && $pass == "teacher") {
	header("Location:teacher.php?user=".$user);
}
else {
	echo "<script type=\"text/javascript\">window.alert('Invalid User!!');window.location.href = 'index.html';</script>"; 
   	exit;
}
?>
