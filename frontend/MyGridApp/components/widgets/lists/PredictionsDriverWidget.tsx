import { Constants, GlobalStyles } from "@/theme";
import { TouchableOpacity, TouchableOpacityProps } from "react-native"
import { MainText, SpotLight } from "@/components/widgets";

export function PredictionsDriverWidget ({
  item=null,
  ...otherProps
} : {
  item: any
} & TouchableOpacityProps) {

  return (
    <TouchableOpacity style={[GlobalStyles.button, GlobalStyles.driverWidget]} {...otherProps}>
      <SpotLight color={item.team.color} cx="60%" cy="65%" fx="85%" fy="85%" radius="70%"/>
      <MainText style={{ fontSize: Constants.fontSizes.header, marginLeft: Constants.spacing.buttonPadding }} bold={true}>{item?.driver?.lastname}</MainText>
      {/*<MainText style={{ fontSize: Constants.fontSizes.header, marginRight: Constants.spacing.buttonPadding }}>+ {item?.score}</MainText>*/}
    </TouchableOpacity>
  )
}