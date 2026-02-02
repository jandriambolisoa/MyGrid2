import { Container, MainText } from "@/components/widgets";
import { ScrollView } from "react-native";

export default function Events () {

  return (
    <Container>
      <ScrollView>
      {
        Array.from({ length: 50 }, (_, i) => (
          <MainText key={i}>Home Screen Line {i + 1}</MainText>
        ))
      }
      </ScrollView>
    </Container>
  )
}