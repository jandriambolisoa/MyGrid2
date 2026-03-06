import { View } from "react-native";
import { ProfilePicture, SpotLight, MainText } from "@/components/widgets";
import { Constants, GlobalStyles } from "@/theme";
import { scopedI18n } from "@/translations/i18n";

export function RankingsUserWidget ({
  item=null,
  spotColor=null,
  you=false
} : {
  item: any | null;
  spotColor?: string | null;
  you?: boolean;
}) {

  const t = scopedI18n('rankings')

  return (
    <View style={[GlobalStyles.button, { height: Constants.spacing.userWidgetHeight }]}>
      {spotColor && <SpotLight color={spotColor} cx="60%" cy="60%" fx="80%" fy="80%" radius="70%" opacityStart="0.8"/>}
      <View style={{ flexDirection: 'row', paddingHorizontal: Constants.spacing.listMargin }}>
        <ProfilePicture link={item?.user?.image_url} borders={true} style={{ marginEnd: Constants.spacing.listMargin }}/>
        <View style={{ flex: 1, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingStart: Constants.spacing.listMargin }}>
          <MainText bold={you}>{you? t('you') : item?.user?.username}</MainText>
          <MainText fontSize='header'>{item?.score} {t('pts')}</MainText>
        </View>
      </View>
    </View>
  )
}