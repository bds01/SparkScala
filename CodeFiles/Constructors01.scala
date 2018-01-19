
class Person01 (val firstName:String, val lastName:String, val Age:Int){
       def this(firstName: String, lastName: String){
         this(firstName, lastName, 0)
       }
       
       def this(firstName: String){
         this(firstName, "", 0)
       }
       
       def this(){
         this("","",0)
       }      
       
       override def toString: String = {
         return "%s %s, age %d".format(firstName, lastName, Age)
       }
}

object Constructors01 {
    def main(args: Array[String]) {
      val p1 = new Person01("Patrick","Peterson",45)
      val p2 = new Person01("Patrick","Peterson")
      val p3 = new Person01("Patrick")
      val p4 = new Person01()

      println(p1)
      println(p2)
      println(p3)
      println(p4)
      
    } 
}