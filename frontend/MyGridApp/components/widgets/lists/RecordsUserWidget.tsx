import { scopedI18n } from "@/translations/i18n";
import { useRouter } from "expo-router";
import { Colors, Constants, GlobalStyles } from "@/theme";
import { View } from "react-native";
import { MainText, SpotLight, ProfilePicture } from "@/components/widgets";

export function RecordsUserWidget ({
  item=null,
  you=false,
} : {
  item: any;
  you?: boolean;
}) {

  const t = scopedI18n('rankings');

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
      <View style={[GlobalStyles.button, { flex: 1 }]}>
        <SpotLight color={color} cx="60%" cy="60%" fx="80%" fy="80%" radius="70%" opacityStart="0.8" opacityEnd="0.1"/>
        <View style={{ flexDirection: 'row', padding: Constants.spacing.listMargin, alignItems: 'center' }}>
          
          <ProfilePicture link={item?.user?.image_url} borders={true} style={{ marginEnd: Constants.spacing.listMargin }}/>
          <View style={{ flex: 1, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingStart: Constants.spacing.listMargin }}>
            <MainText>{item?.user?.username}</MainText>
          </View>
          <MainText fontSize='header'>{item?.score} {t('pts')}</MainText>
        </View>
        
      </View>
    </View>
  )
}