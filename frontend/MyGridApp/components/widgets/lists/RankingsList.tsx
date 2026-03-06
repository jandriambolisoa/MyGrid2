import { ScrollContainer, Separator, NumbersList, RankingsUserWidget } from "@/components/widgets";
import { FlatList, View } from "react-native";

export function RankingsList ({
  datas=[],
  footerHeight,
  headerHeight
}: {
  datas: any;
  footerHeight: number;
  headerHeight: number;
}) {

  function renderItem (item: any) {

    return (
      <RankingsUserWidget item={item}/>
    )
  }

  return (
    <ScrollContainer footerHeight={footerHeight} headerHeight={headerHeight}>
      <NumbersList numbers={datas.length} />
      <View style={{ width: '85%' }}>
        <FlatList
          data={datas}
          renderItem={({item}) => renderItem(item)}
          scrollEnabled={false}
          ItemSeparatorComponent={() => Separator}
        />
      </View>
    </ScrollContainer>
  )
}