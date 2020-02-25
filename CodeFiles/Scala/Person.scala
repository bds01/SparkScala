

class Person(var firstName: String, var lastName: String) {
  println("the constructor begins")
  
  private val HOME =System.getProperty("user.home")
  var age = 0
  
  override def toString = s"$firstName $lastName is $age years old"
  def printHome {println(s"HOME = $HOME") }
  def printFullName {println(this)}
  
  printHome
  printFullName
  println("still in the constructor")
  
  def fullName(age:Int){
    println(s"The full name is $firstName, $lastName and he/she is $age years old")
  }
}
