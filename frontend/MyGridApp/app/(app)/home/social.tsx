import { Container, MainText, SpotLight } from "@/components/widgets";
import { Colors, Constants } from "@/theme";
import { FontAwesome6 } from "@expo/vector-icons";
import { View } from "react-native";

export default function Social () {
  return (
    <Container >
      <View style={{ height: '80%', alignSelf: 'stretch', justifyContent: 'center', alignItems: 'center' }}>
        <SpotLight color={Colors.light.orangeLogo} cx="65%" cy="40%" fx="65%" fy="40%" radius="35%"/>
        <SpotLight color={Colors.light.cyanLogo} cx="35%" cy="60%" fx="35%" fy="60%" radius="35%"/>
        <FontAwesome6 name='gears' color={Colors.light.lightText} size={30}/>
        <MainText style={{ fontSize: Constants.fontSizes.header, marginVertical: 16 }} bold={true}>Work in progress...</MainText>
        <MainText style={{ maxWidth: '80%' }}>Leaderboards will be alvailable after the first session of the season, stay tuned!</MainText>
      </View>
    </Container>
  )
}