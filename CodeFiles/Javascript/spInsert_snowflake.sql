CREATE TABLE test.tgtResults
( sRegulatoryEntity VARCHAR(50) NULL,
  sEntity VARCHAR(50) NULL,
  sTradingGroup VARCHAR(50) NULL
);

create or replace procedure test.get_results()
    returns varchar not null
    language javascript
    as
    $$
	var return_value = "";
    var col1, col2, col3, insert_res;
      
	var SQL_STMT = "SELECT DISTINCT TOP 3 \"Regulatory Entity\", Entity, \"Trading Group\" FROM DEV_STAGE_FILE.SRC_RISKCUBE.TRADEBOOKDIM" ;
    var stmt = snowflake.createStatement({sqlText: SQL_STMT});
	/* Creates result set */
	var res = stmt.execute();
	
    while (res.next())  {
       for (i=3; i>=1; i--) {      
        if (i>=1) {col1 = res.getColumnValue(1)} else {col1 = null};
        if (i>=2) {col2 = res.getColumnValue(2)} else {col2 = null};
        if (i>=3) {col3 = res.getColumnValue(3)} else {col3 = null};

        var SQL_INSERT = "INSERT INTO test.tgtResults (sRegulatoryEntity, sEntity, sTradingGroup) VALUES ('"+col1+"', '"+col2+"', '"+col3+"')";
        var stmt_insert = snowflake.createStatement({sqlText: SQL_INSERT})  
        var insert_res = stmt_insert.execute();
            }     
        }
    return return_value;    
	$$
	;
    
call test.get_results();
