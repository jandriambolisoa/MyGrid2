import { TouchableOpacity, View } from "react-native";
import { ProfilePicture, SpotLight, MainText } from "@/components/widgets";
import { Colors, Constants, GlobalStyles } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { useRouter } from "expo-router";

export function RankingsUserWidget ({
  item=null,
  spotColor=null,
  you=false,
  event=null
} : {
  item: any | null;
  spotColor?: string | null;
  you?: boolean;
  event?: any;
}) {

  const t = scopedI18n('rankings')
  const router = useRouter();

  // Replacing color - tmp
  const color = you ? Colors.light.warning : "#03051F"

  return (
    <View style={{
      paddingHorizontal: Constants.spacing.listMargin,
      paddingVertical: Constants.spacing.listMargin / 2,
      flexDirection: 'row'
    }}>
      <View style={{ alignItems: 'center', justifyContent: 'center', paddingHorizontal: Constants.spacing.listMargin, minWidth: Constants.spacing.listNumber }}>
        <MainText fontSize="header" bold={true}>{item.rank}</MainText>
      </View>
      <TouchableOpacity
        style={[GlobalStyles.button, { height: Constants.spacing.userWidgetHeight, flex: 1 }]}
        onPress={() => router.push({
          pathname: `/rankings/search/${item?.user?.id}` as any,
          params: {
            event: JSON.stringify(event),
            item: JSON.stringify(item)
          }
        })}
      >
        {spotColor && <SpotLight color={color} cx="60%" cy="60%" fx="80%" fy="80%" radius="70%" opacityStart="0.8" opacityEnd="0.1"/>}
        <View style={{ flexDirection: 'row', paddingHorizontal: Constants.spacing.listMargin }}>
          <ProfilePicture link={item?.user?.image_url} borders={true} style={{ marginEnd: Constants.spacing.listMargin }}/>
          <View style={{ flex: 1, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingStart: Constants.spacing.listMargin }}>
            <MainText>{item?.user?.username}</MainText>
            <MainText fontSize='header'>{item?.score} {t('pts')}</MainText>
          </View>
        </View>
      </TouchableOpacity>
    </View>
  )
}