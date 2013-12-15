<?php
date_default_timezone_set('PRC');
$time = date( "Y-m-d g:i a"); 
$thnsv2cookie=$_GET["t"];
$jsessionid=$_GET["j"];
$ip= $_SERVER["REMOTE_ADDR"];

$con = mysql_connect("localhost","root","raspberry");
mysql_select_db("learn", $con);

$result = mysql_query("SELECT * FROM visitor");
while($row = mysql_fetch_array($result))
  {
  echo "time: ",$row['time'],"<br />";
  echo "visitor: ",$row['ip'],"<br />";
  echo "thnsv2cookie:<br/>",$row['thnsv2cookie'],"<br />";
 echo "jsessionid:<br/>",$row['jsessionid'],"<br /><br />";
  }


if($thnsv2cookie!=NULL && $jsessionid!=NULL){
mysql_query("INSERT INTO visitor (ip,thnsv2cookie, jsessionid,time) VALUES ('$ip','$thnsv2cookie','$jsessionid','$time');");
}
mysql_close($con);

?>
