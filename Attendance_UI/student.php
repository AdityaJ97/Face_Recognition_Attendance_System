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
		echo "<form action='student.php' action='get'>";
		echo '<input type="hidden" name="user" value="'.$_GET['user'].'">';
		echo 'Enter MIS : <input type="text" name="mis">';
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
		echo '<input type="submit" value="Get Attendance">';
		echo "<br>";
		if(isset($_GET["mis"])) {
			
			$mis = $_GET["mis"];
			$subject = $_GET["subject"];
			$month = $_GET["month"];
			$query = "select * from ".$subject."_".$month." where mis = ".$mis;
			$result = $conn->query($query);
			if ($result->num_rows > 0) {
    			$row = $result->fetch_assoc();
    			for($i = 1; $i <= 31; $i++ ) {
    				if($row[$i] == 0)
    					echo $i. " A";
    				else
    					echo $i. " P - " . $row[$i];
				echo "<br>";
			}
			

			}
		}
		
		echo '</div>
	</div>
	</body>';
?>
