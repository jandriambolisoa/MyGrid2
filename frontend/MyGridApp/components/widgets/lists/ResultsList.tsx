import { FlatList, View } from "react-native"
import { ShortDriverWidget, ResultsDriverWidget, NumbersList, Separator } from "@/components/widgets"
import { Constants } from "@/theme"

export type ResultsListProps = {
  datas?: any[]
}

export function ResultsList ({
  datas=[]
}: ResultsListProps) {

  const leftDatas = [...datas].sort((a: any, b: any) => {
    return a.result - b.result
  })

  function leftRenderItem (item: any) {
    return (
      <ShortDriverWidget item={item}/>
    )
  }

  function rightRenderItem (item: any) {
    return (
      <ResultsDriverWidget item={item}/>
    )
  }

  return (
    <View style={{ flexDirection: 'row', padding: Constants.spacing.listMargin }}>
      <FlatList
        data={leftDatas}
        renderItem={({item}) => leftRenderItem(item)}
        scrollEnabled={false}
        ItemSeparatorComponent={() => Separator}
      />
      <NumbersList numbers={datas.length}/>
      <View style={{ width: Constants.spacing.driverWidgetWidth as any }}>
        <FlatList
          data={datas}
          renderItem={({item}) => rightRenderItem(item)}
          scrollEnabled={false}
          ItemSeparatorComponent={() => Separator}
        />
      </View>
    </View>
  )
}