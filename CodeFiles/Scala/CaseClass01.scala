

case class CaseClass01(firstName: String, lastName: String)

object Person01 {
  def main(args: Array[String]) {
val me1 = CaseClass01("Daniel", "Spiewak")
val me2 = CaseClass01("Daniel", "Speiwak")
val first = me1.firstName
val last = me1.lastName
 
if (me2 == CaseClass01(first, last)) {
  println("Found myself!")
  println(me1)
  println(me2)
  }
else {
  println("Match not found")
  }
}
  }
