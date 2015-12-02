<?php 

if (isset($_POST['submit'])) {
    print "<h1> Clint Cooper & Emily Rohrbough ~ Recipe Database </h1><br>";

    $link = mysqli_connect("localhost", "root", "<replace>", "Recipes");

    if ($link === false){
        die("Error: Could not connect. " . mysqli_connect_error());
    }

    $sql = isset($_POST['input']) ? $_POST['input'] : '';

    echo $query;

    $result = mysqli_query($link, $sql) or die(mysqli_error());
    print "Input Query:<br>";
    print "$sql<br>";
    print "<br>Results:<br>";
    print "<table border='1'>";
    while($row = mysqli_fetch_assoc($result)){
        print "<tr>";
        foreach($row as $cname => $cvalue){
            print "<td>$cname:<br>$cvalue</td>";
        }
        print "</tr>";
    }
    print "</table>";

} else {
    print "<h1> Clint Cooper & Emily Rohrbough ~ Recipe Database </h1><br>";

    $link = mysqli_connect("localhost", "root", "<replace>", "Recipes");

    if ($link === false){
        die("Error: Could not connect. " . mysqli_connect_error());
    }

    $sql = "SELECT R.Name
            FROM RECIPE R, AMOUNT_REQUIRED A
            WHERE R.Recipe_No = A.Recipe_No 
            AND A.Ingredient_No IN (SELECT Ingredient_No
                                    FROM INGREDIENT
                                    WHERE NAME LIKE '%chicken%')";

    $result = mysqli_query($link, $sql) or die(mysqli_error());

    print "$sql<br>";
    print "<table border='1'>";
    while($row = mysqli_fetch_assoc($result)){
        print "<tr>";
        foreach($row as $cname => $cvalue){
            print "<td>$cname:<br>$cvalue</td>";
        }
        print "</tr>";
    }
    print "</table><br><br><br>";

    $sql = "SELECT R.Name
            FROM RECIPE R
            WHERE (R.Calories / R.Quantity) < 500
            LIMIT 5";

    $result = mysqli_query($link, $sql) or die(mysqli_error());

    print "$sql<br>";
    print "<table border='1'>";
    while($row = mysqli_fetch_assoc($result)){
        print "<tr>";
        foreach($row as $cname => $cvalue){
            print "<td>$cname:<br>$cvalue</td>";
        }
        print "</tr>";
    }
    print "</table><br><br><br>";

    $sql = "SELECT DISTINCT R.Name
            FROM RECIPE R, SOURCE S
            WHERE S.Reference LIKE '%allrecipes.com%'
            LIMIT 5";

    $result = mysqli_query($link, $sql) or die(mysqli_error());

    print "$sql<br>";
    print "<table border='1'>";
    while($row = mysqli_fetch_assoc($result)){
        print "<tr>";
        foreach($row as $cname => $cvalue){
            print "<td>$cname:<br>$cvalue</td>";
        }
        print "</tr>";
    }
    print "</table><br><br><br>";

    $sql = "SELECT GROUP_CONCAT(DISTINCT D.Directions SEPARATOR ', ') as 'Directions', GROUP_CONCAT(I.Name, ' : ', A.Amount, ' ', A.Unit SEPARATOR '<br>') as 'Ingredients' 
            FROM INSTRUCTION_LIST D, INGREDIENT I JOIN AMOUNT_REQUIRED A ON I.Ingredient_No = A.Ingredient_No, RECIPE R 
            WHERE R.Name LIKE 'Chicken Enchiladas%' AND D.Direction_No = R.Recipe_No AND A.Recipe_No = R.Recipe_No";

    $result = mysqli_query($link, $sql) or die(mysqli_error());

    print "$sql<br>";
    print "<table border='1'>";
    print "<col width = '50%'";
    print "<col width = '50%'";
    while($row = mysqli_fetch_assoc($result)){
        print "<tr>";
        foreach($row as $cname => $cvalue){
            print "<td>$cname:<br>$cvalue</td>";
        }
        print "</tr>";
    }
    print "</table><br><br><br>";

    $sql = "SELECT R.Name as 'Recipe Name', I.Name as 'Possible Gluten Ingredient'
            FROM RECIPE R,
                 (SELECT A.Recipe_No, SUM(I.Contains_Glutten) as Gluten
                  FROM INGREDIENT I JOIN AMOUNT_REQUIRED A on I.Ingredient_No = A.Ingredient_No
                  GROUP BY A.Recipe_No) T,
                 INGREDIENT I JOIN AMOUNT_REQUIRED A on I.Ingredient_No = A.Ingredient_No
            WHERE T.Gluten < '2'
            AND T.Recipe_No = R.Recipe_No
            AND A.Recipe_No = R.Recipe_No
            AND I.Contains_Glutten = 1
            LIMIT 25";

    $result = mysqli_query($link, $sql) or die(mysqli_error());

    print "$sql<br>";
    print "<table border='1'>";
    while($row = mysqli_fetch_assoc($result)){
        print "<tr>";
        foreach($row as $cname => $cvalue){
            print "<td>$cname:<br>$cvalue</td>";
        }
        print "</tr>";
    }
    print "</table><br><br><br>";
?>

<form action="<?php echo basename(__FILE__); ?>" method="post">
<h3><label for="input">Enter a query:</label></h3>
<input type="text" id="input" name="input" size="50" maxlength="2000" value="" />

</fieldset>
<p class="button"><input class="submit" type="submit" name="submit" value="Submit Query" /></p>
</form>

<?php
}
?>