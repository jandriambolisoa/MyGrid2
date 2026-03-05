import { Constants, GlobalStyles } from "@/theme";
import { TouchableOpacity, TouchableOpacityProps } from "react-native"
import { MainText, SpotLight } from "@/components/widgets";
import { scopedI18n } from "@/translations/i18n";
import { computeScore } from "@/utils";

export function PredictionsDriverWidget ({
  item=null,
  parameters=null,
  ...otherProps
} : {
  item: any,
  parameters: any
} & TouchableOpacityProps) {

  const t = scopedI18n('sessions.predictions')

  // Should be changed if master grid change occurs or other championship is added
  const gridSize = 22;

  return (
    <TouchableOpacity style={[GlobalStyles.button, GlobalStyles.driverWidget]} hitSlop={Constants.spacing.listMargin / 2} {...otherProps}>
      <SpotLight color={item.team.color} cx="60%" cy="65%" fx="85%" fy="85%" radius="70%"/>
      <MainText style={{ fontSize: Constants.fontSizes.header, marginLeft: Constants.spacing.buttonPadding }} bold={true}>{item?.driver?.lastname}</MainText>
      {parameters && <MainText style={{ fontSize: Constants.fontSizes.header, marginRight: Constants.spacing.buttonPadding }}>+ {computeScore(
        item?.mygrid, item?.prediction, gridSize, parameters
      )}</MainText>}
    </TouchableOpacity>
  )
}