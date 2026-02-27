import { FlatList, View } from "react-native"
import { ShortDriverWidget } from "./ShortDriverWidget"
import { MainText } from "../MainText"
import { Constants } from "@/theme"
import { ResultsDriverWidget } from "./ResultsDriverWidget"

export type ResultsListProps = {
  datas?: any[]
}

export function ResultsList ({
  datas=[]
}: ResultsListProps) {

  const numberDatas = Array.from({ length: 22 }, (_, i) => ({
    id: (i + 1).toString(),
    value: i + 1,
  }))

  const leftDatas = [...datas].sort((a: any, b: any) => {
    return a.result - b.result
  })

  function leftRenderItem (item: any) {
    return (
      <ShortDriverWidget item={item}/>
    )
  }

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

  function rightRenderItem (item: any) {
    return (
      <ResultsDriverWidget item={item}/>
    )
  }

  const separator = <View style={{ height: Constants.spacing.listMargin }}/>

  return (
    <View style={{ flexDirection: 'row', padding: Constants.spacing.listMargin }}>
      <FlatList
        data={leftDatas}
        renderItem={({item}) => leftRenderItem(item)}
        scrollEnabled={false}
        ItemSeparatorComponent={() => separator}
      />
      <FlatList
        data={numberDatas}
        renderItem={({item}) => numberRenderItem(item)}
        scrollEnabled={false}
        ItemSeparatorComponent={() => separator}
      />
      <View style={{ width: Constants.spacing.driverWidgetWidth as any }}>
        <FlatList
          data={datas}
          renderItem={({item}) => rightRenderItem(item)}
          scrollEnabled={false}
          ItemSeparatorComponent={() => separator}
        />
      </View>
    </View>
  )
}