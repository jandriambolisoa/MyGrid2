import { View, FlatList } from "react-native"
import { MainText, ResultsListProps, ResultsDriverWidget } from "@/components/widgets";
import { Constants } from "@/theme"

export function ResultsAlonelist ({
  datas=[]
}: ResultsListProps) {

  const numberDatas = Array.from({ length: 22 }, (_, i) => ({
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

  function renderItem (item: any) {

    return (
      <ResultsDriverWidget item={item} />
    )
  }

  const separator = <View style={{ height: Constants.spacing.listMargin }}/>

  return (
    <View style={{ flexDirection: 'row', padding: Constants.spacing.listMargin }}>
      <FlatList
        data={numberDatas}
        renderItem={({item}) => numberRenderItem(item)}
        scrollEnabled={false}
        ItemSeparatorComponent={() => separator}
      />
      <View style={{ width: Constants.spacing.driverWidgetWidthWide as any }}>
        <FlatList
          data={datas}
          renderItem={({item}) => renderItem(item)}
          scrollEnabled={false}
          ItemSeparatorComponent={() => separator}
        />
      </View>
    </View>
  )
}