import { View, FlatList } from "react-native"
import { ResultsListProps, ResultsDriverWidget, Separator, NumbersList } from "@/components/widgets";
import { Constants } from "@/theme"

export function ResultsAlonelist ({
  datas=[]
}: ResultsListProps) {

  function renderItem (item: any) {

    return (
      <ResultsDriverWidget item={item} />
    )
  }

  return (
    <View style={{ flexDirection: 'row', padding: Constants.spacing.listMargin }}>
      <NumbersList numbers={datas.length}/>
      <View style={{ width: Constants.spacing.driverWidgetWidthWide as any }}>
        <FlatList
          data={datas}
          renderItem={({item}) => renderItem(item)}
          scrollEnabled={false}
          ItemSeparatorComponent={() => Separator}
        />
      </View>
    </View>
  )
}