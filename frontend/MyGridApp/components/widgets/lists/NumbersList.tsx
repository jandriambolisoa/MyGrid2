import { View, FlatList } from "react-native"
import { Constants } from "@/theme"
import { MainText, Separator } from "@/components/widgets"

export function NumbersList ({
  numbers=0
} : {
  numbers?: number
}) {

  const numberDatas = Array.from({ length: numbers }, (_, i) => ({
    id: (i + 1).toString(),
    value: i + 1,
  }))

  function numberRenderItem (item: any) {
    return (
      <View style={{
        height: Constants.spacing.driverWidgetHeight,
        width: Constants.spacing.driverWidgetHeight,
        alignItems: 'center',
        justifyContent: 'center',
        alignSelf: 'center'
      }}>
        <MainText style={{ fontSize: Constants.fontSizes.header }} bold={true}>{item.value}</MainText>
      </View>
    )
  }

  return (
    <FlatList
      data={numberDatas}
      renderItem={({item}) => numberRenderItem(item)}
      scrollEnabled={false}
      ItemSeparatorComponent={() => Separator}
    />
  )
}