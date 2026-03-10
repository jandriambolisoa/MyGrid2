import { FlatList, View } from "react-native";
import { MainText, ScrollContainer, SpotLight } from "@/components/widgets";
import { Constants, GlobalStyles } from "@/theme";

export function UserPredictionsList ({
  datas=[],
  footerHeight=0,
  headerHeight=0,
} : {
  datas: any;
  footerHeight?: number;
  headerHeight?: number;
}) {

  function renderItem (item: any) {

    const color1 = item?.event_colors[0];
    const color2 = item?.event_colors.length > 1 ? datas?.event.colors[1] : color1;

    return (
      <View style={[GlobalStyles.button, { marginHorizontal: Constants.spacing.listMargin, marginVertical: Constants.spacing.listMargin / 2 }]}>
        <SpotLight color={color1}/>
        <MainText>{item?.name}</MainText>
      </View>
    )
  }

  return (
    <FlatList
      data={datas}
      renderItem={({item}) => renderItem(item)}
      style={{ 
        paddingTop: headerHeight,
        paddingBottom: footerHeight
      }}
    />
  )
}