import { FlatList, TouchableOpacity, View } from "react-native";
import { MainText, SpotLight } from "@/components/widgets";
import { Constants, GlobalStyles } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { useRouter } from "expo-router";

export function UserPredictionsList ({
  datas=[],
  footerHeight=0,
  headerHeight=0,
  userId=0
} : {
  datas: any;
  footerHeight?: number;
  headerHeight?: number;
  userId?: number;
}) {

  const t = scopedI18n('rankings')
  const router = useRouter();

  function renderItem (item: any) {

    const color = item?.event_colors[0];

    return (
      <TouchableOpacity
        style={[GlobalStyles.button, { marginHorizontal: Constants.spacing.listMargin, marginVertical: Constants.spacing.listMargin / 2 }]}
        onPress={() => router.push({
          pathname: `/rankings/results/${userId}/${item?.id}` as any
        })}
      >
        <SpotLight color={color} cx="60%" cy="65%" fx="85%" fy="85%" radius="70%"/>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignSelf: 'stretch', paddingHorizontal: Constants.spacing.buttonPadding }}>
          <MainText>{item?.name}</MainText>
          <MainText>{item?.score} {t('pts')}</MainText>
        </View>
      </TouchableOpacity>
    )
  }

  return (
    <FlatList
      data={datas}
      renderItem={({item}) => renderItem(item)}
      style={{ 
        paddingTop: headerHeight +  Constants.spacing.listMargin / 2,
        paddingBottom: footerHeight + Constants.spacing.listMargin / 2
      }}
    />
  )
}