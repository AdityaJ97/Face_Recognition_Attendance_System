<?php
include 'dbconfig.php';
	
echo '<head>
	<title>Attendance</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="css/util.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">	
</head>';
echo '<body>
	
	<div class="limiter">
		<div class="container-show">';
		echo "<h2>Hello ". $_GET['user']."</h2>";
		echo "<br><br>";
		echo "<form action='teacher.php' action='get'>";
		echo '<input type="hidden" name="user" value="'.$_GET['user'].'">';
		echo "<br><br>";
		echo 'Select Subject : <select name="subject">
		<option value="SE">SE</option>
		<option value="os">OS</option>
		<option value="ds">DSCI</option>
		<option value="ai">AI</option>
		<option value="dbms">DBMS</option>
		</select>'; 
		echo "<br><br>";
		echo 'Select Month : <select name="month">
		<option value="1">1</option>
		<option value="2">2</option>
		<option value="3">3</option>
		<option value="4">4</option>
		<option value="5">5</option>
		<option value="6">6</option>
		<option value="7">7</option>
		<option value="8">8</option>
		<option value="9">9</option>
		<option value="10">10</option>
		<option value="11">11</option>
		<option value="12">12</option>
		</select>'; 
		echo "<br><br>";
		echo 'Select Day : <select name="day">
		<option value="1">1</option>
		<option value="2">2</option>
		<option value="3">3</option>
		<option value="4">4</option>
		<option value="5">5</option>
		<option value="6">6</option>
		<option value="7">7</option>
		<option value="8">8</option>
		<option value="9">9</option>
		<option value="10">10</option>
		<option value="11">11</option>
		<option value="12">12</option>
		<option value="13">13</option>
		<option value="14">14</option>
		<option value="15">15</option>
		<option value="16">16</option>
		<option value="17">17</option>
		<option value="18">18</option>
		<option value="19">19</option>
		<option value="20">20</option>
		<option value="21">21</option>
		<option value="22">22</option>
		<option value="23">23</option>
		<option value="24">24</option>
		<option value="25">25</option>
		<option value="26">26</option>
		<option value="27">27</option>
		<option value="28">28</option>
		<option value="29">29</option>
		<option value="30">30</option>
		<option value="31">31</option>
		</select>'; 
		echo "<br><br>";
		echo '<input type="submit" value="Get Attendance">';
		echo "<br>";
		if(isset($_GET["subject"])) {
			
			$subject = $_GET["subject"];
			$month = $_GET["month"];
			$day = $_GET["day"];
			$query = "select mis , `".$day."` from ".$subject."_".$month;
			$result = $conn->query($query);
			if ($result->num_rows > 0) {
    			while($row = $result->fetch_assoc()) {
    				echo $row["mis"] . " -> " .$row[$day];
    				echo "<br>"; 
			}
			

			}
		}
		
		echo '</div>
	</div>
	</body>';
?>
