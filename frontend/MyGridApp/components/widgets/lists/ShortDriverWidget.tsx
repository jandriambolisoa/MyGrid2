import { Constants, GlobalStyles } from "@/theme";
import { View } from "react-native"
import { MainText, SpotLight } from "@/components/widgets";

export function ShortDriverWidget ({
  item=null,
} : {
  item: any
}) {

  return (
    <View style={[GlobalStyles.button, { height: Constants.spacing.driverWidgetHeight }]}>
      <SpotLight color="#ff2200" cx="35%" cy="35%" fx="5%" fy="5%" radius="60%"/>
      <MainText style={{ fontSize: Constants.fontSizes.header }} bold={true}>{item?.driver?.codename}</MainText>
    </View>
  )
}