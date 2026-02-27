import { MainText } from '@/components/widgets'
import { Constants } from '@/theme'
import { View } from "react-native"

export function ResultsLabels () {

  return (
    <View style={{ flexDirection: 'row', paddingHorizontal: Constants.spacing.listMargin, marginBottom: Constants.spacing.listMargin }}>
      <MainText style={{ flex: 1 }}>F1</MainText>
      <MainText style={{ width: Constants.spacing.driverWidgetHeight * 1.5 }}>Pos</MainText>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', width: Constants.spacing.driverWidgetWidth as any, paddingHorizontal: Constants.spacing.mainWidgetMargin }}>
        <MainText>My Grid</MainText>
        <MainText>Points</MainText>
      </View>
    </View>
  )
}