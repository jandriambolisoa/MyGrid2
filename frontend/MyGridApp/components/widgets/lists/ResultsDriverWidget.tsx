import { Constants, GlobalStyles } from "@/theme";
import { View } from "react-native"
import { MainText, SpotLight } from "@/components/widgets";

export function ResultsDriverWidget ({
  item=null,
} : {
  item: any
}) {

  return (
    <View style={[GlobalStyles.button, GlobalStyles.driverWidget]}>
      <SpotLight color="#ff2200" cx="60%" cy="65%" fx="85%" fy="85%" radius="70%"/>
      <MainText style={{ fontSize: Constants.fontSizes.header, marginLeft: Constants.spacing.buttonPadding }} bold={true}>{item?.driver?.lastname}</MainText>
      <MainText style={{ fontSize: Constants.fontSizes.header, marginRight: Constants.spacing.buttonPadding }}>{item?.score} Pts</MainText>
    </View>
  )
}