import { ScrollContainer, Separator, NumbersList, RankingsUserWidget } from "@/components/widgets";
import { Constants } from "@/theme";
import { FlatList, View } from "react-native";
import { useAuth } from '@/contexts/AuthContext'
import { useEffect } from "react";

export function RankingsList ({
  datas=[],
  footerHeight=0,
  headerHeight=0,
  color=null,
}: {
  datas: any;
  footerHeight?: number;
  headerHeight?: number;
  color?: string | null;
}) {

  const { user } = useAuth()

  function renderItem (item: any) {

    const you = user?.username === item?.user?.username ? true : false

    return (
      <RankingsUserWidget item={item} spotColor={color} you={you}/>
    )
  }

  useEffect(() => {
    console.log(datas)
  }, [datas])

  return (
    <ScrollContainer footerHeight={footerHeight} headerHeight={headerHeight}>
      <View style={{ flexDirection: 'row', padding: Constants.spacing.listMargin }}>
      <NumbersList numbers={datas.length} contentContainerStyle={{ paddingEnd: 4 }} itemHeight={Constants.spacing.userWidgetHeight}/>
        <View style={{ width: '90%' }}>
          <FlatList
            data={datas}
            renderItem={({item}) => renderItem(item)}
            scrollEnabled={false}
            ItemSeparatorComponent={() => Separator}
          />
        </View>
      </View>
    </ScrollContainer>
  )
}