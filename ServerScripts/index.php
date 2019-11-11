<?php
$con = mysqli_connect("18.218.244.52", "simha", "simha183simha", "speeddata");
// Check connection
if (mysqli_connect_errno()) 
{
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
    exit();
}

$max_speed = 0;

if ($_GET["lat"] && $_GET["lon"]) 
{
    $lat = $_GET["lat"];
    $lon = $_GET["lon"];

    $query = "SELECT * FROM speed WHERE lat BETWEEN " . ($lat - 1) . " AND " . ($lat + 1);
    $results = mysqli_query($con, $query);
    if ($results) 
    {
        $temp_speeds = array();
        // Fetch one and one row
        while ($row = mysqli_fetch_assoc($results)) 
        {
            if ($row[lon] > ($lon - 1) && $row[lon] < ($lon + 1)) 
            {
                array_push($temp_speeds, $row);
            }
        }
        
        if (count($temp_speeds) <= 0) 
        {
            $max_speed = -1;
        } 
        else 
        {
            $temp_dist = 9999;
            foreach ($temp_speeds as $speed) 
            {
                $lat_diff_sq = pow(($lat - $speed['lat']), 2);
                $lon_diff_sq = pow(($lon - $speed['lon']), 2);
                $current_dist = pow(($lat_diff_sq + $lon_diff_sq), 0.5);
                // echo ($temp_dist . "                " . $current_dist . "              ");
                if($current_dist < $temp_dist)
                {
                    $temp_dist = $current_dist;
                    $max_speed = (int)$speed['max_speed'];
                    // echo ("<br>");echo($speed['lat']);echo ("<br>");echo ("<br>");
                }
                // echo ($speed['lat'] . "     " . $speed['lon'] . "     " . $speed['max_speed']);
                // echo ("<br>");
            }
        }

        // Free result set
        mysqli_free_result($result);
    }
} 
else if (($_GET["lat"] && !($_GET["lon"])) || (!($_GET["lat"]) && $_GET["lon"])) 
{
    $max_speed = -1;
}

echo json_encode($max_speed);
mysqli_close($con);

?>