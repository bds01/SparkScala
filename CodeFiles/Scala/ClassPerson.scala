

case class ClassPerson (var name: String, var age:Int)

object ClassPerson {
  def apply() = new ClassPerson("<no name>", 0)
  def apply(name: String) = new ClassPerson(name, 0)
}


object CaseClassTest extends App {
val a = ClassPerson() // corresponds to apply()
val b = ClassPerson("Pam") // corresponds to apply(name: String)
val c = ClassPerson("William Shatner", 82)
println(a)
println(b)
println(c)
// verify the setter methods work
a.name = "Leonard Nimoy"
a.age = 82
println(a)
}
