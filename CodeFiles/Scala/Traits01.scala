trait T1{
  def add():Int
  def subract():Int
  def multiply():Int
}

class Child(val x:Int, val y:Int) extends T1 {
  
  override def add:Int = x+y
  override def subract:Int = x-y
  override def multiply:Int = x*y
}

object Traits01 {
    def main(args:Array[String]):Unit = {
      val p = new Child(7,3)
           
      println(s"The sum of ${p.x} and ${p.y} is ${p.add()}")
      println(s"${p.x} minus ${p.y} is ${p.subract()}")
      println(s"The product of ${p.x} and ${p.y} is ${p.multiply()}")
    }
}
