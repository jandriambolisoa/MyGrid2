import { useEffect, useRef } from "react";
import { Animated } from "react-native";

export function Reaction ({item} : {item: any}) {

  const translateX = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(0)).current;
  const randScale = useRef(new Animated.Value(0)).current;
  const randRot = useRef(new Animated.Value(0)).current;

useEffect(() => {
  let mounted = true;

  const animate = () => {
    if (!mounted) return;

    // reset Y
    translateY.setValue(35);

    // nouvelles valeurs aléatoires
    translateX.setValue(Math.random() * 100 - 50);
    randScale.setValue(Math.random() / 2 + 1);
    randRot.setValue(Math.random() * 20 - 10);

    // animation Y
    Animated.timing(translateY, {
      toValue: -35,
      duration: 3000 + Math.random() * 2000,
      useNativeDriver: true,
    }).start(() => {
      animate(); // relance la boucle
    });
  };

  const initialDelay = Math.random() * 3000; // entre 0 et 1 seconde
  const timeout = setTimeout(() => {
    animate();
  }, initialDelay);

  return () => {
    mounted = false; // stoppe la boucle si le composant se démonte
    clearTimeout(timeout);
  };
}, []);

  return (
    <Animated.Text
      style={{
        position: "absolute",
        left: "45%",
        transform: [
          { translateX: translateX },
          { translateY: translateY },
          { scale: randScale },
          {
            rotate: randRot.interpolate({
              inputRange: [-10, 10],
              outputRange: ["-10deg", "10deg"],
            }),
          },
        ],
      }}
    >
      {item.reaction}
    </Animated.Text>
  );
}