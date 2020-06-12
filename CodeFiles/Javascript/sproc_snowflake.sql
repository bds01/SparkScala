create or replace procedure test.get_results()
    returns varchar not null
    language javascript
    as
    $$
	var return_value = "";
    var text = "";
  //  var level = 3;
	var SQL_STMT = "SELECT DISTINCT TOP 3 \"Regulatory Entity\", Entity, \"Trading Group\" FROM DEV_STAGE_FILE.SRC_RISKCUBE.TRADEBOOKDIM" ;
    var stmt = snowflake.createStatement(
           {
           sqlText: SQL_STMT
           }
        );
	/* Creates result set */
	var res = stmt.execute();
	
    while (res.next())  {
       for (i=3; i>=1; i--) {      
        if (i>=1) {return_value+= res.getColumnValue(1)} else {return_value+="null"};
        if (i>=2) {return_value+= ", " + res.getColumnValue(2)} else {return_value+=", " + "null"};
        if (i>=3) {return_value+= ", " + res.getColumnValue(3)} else {return_value+=", " + "null"};
        //return_value += if (i>=2) {", " + res.getColumnValue(2)} else "";
		//return_value += if (i>=3) {", " + res.getColumnValue(3)+";"} else "";
        return_value += ", level:" + i;
        return_value += "\n";
            }     
        }
    return return_value;    
	$$
	;
  
  call test.get_results();
