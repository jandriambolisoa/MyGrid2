import { ScrollContainer, RankingsUserWidget, RecordsUserWidget } from "@/components/widgets";
import { Constants } from "@/theme";
import { FlatList } from "react-native";
import { useAuth } from '@/contexts/AuthContext'

export function RankingsList ({
  datas=[],
  footerHeight=0,
  headerHeight=0,
  color=null,
  event=null,
  records=false
}: {
  datas: any;
  footerHeight?: number;
  headerHeight?: number;
  color?: string | null;
  event?: any;
  records?: boolean;
}) {

  const { user } = useAuth()

  function renderItem (item: any) {

    const you = user?.username === item?.user?.username ? true : false

    if (records) {
      return (
        <RecordsUserWidget item={item} you={you}/>
      )
    }

    return (
      <RankingsUserWidget item={item} spotColor={color} you={you} event={event}/>
    )
  }

  return (
    <ScrollContainer footerHeight={footerHeight} headerHeight={headerHeight}>
      <FlatList
        data={datas}
        renderItem={({item}) => renderItem(item)}
        scrollEnabled={false}
        contentContainerStyle={{ paddingVertical: Constants.spacing.listMargin / 2 }}
      />
    </ScrollContainer>
  )
}