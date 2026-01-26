import { Colors } from '@/theme/Colors';
import { ReactNode } from 'react';
import { View, type ViewProps, StyleSheet } from 'react-native';
import { Svg, Defs, LinearGradient, RadialGradient, Stop, Rect } from 'react-native-svg';

export type MainWidgetProps = ViewProps & {
  children: ReactNode
  borders?: boolean
  colors?: string[]
};

export function MainWidget({
  style,
  children = null,
  borders = true,
  colors = [],
  ...otherProps
}: MainWidgetProps) {
  return (
    <View style={[styles.widget, style]} {...otherProps}>
      {colors.length > 0 &&
        <Svg height="100%" width="100%" style={StyleSheet.absoluteFill}>
          <Defs>
            <RadialGradient
              id="grad1"
              cx="35%"
              cy="35%"
              r="55%"
              fx="15%"
              fy="15%"
            >
              <Stop offset="0%" stopColor={colors[0]} stopOpacity="0.5" />
              <Stop offset="100%" stopColor={colors[0]} stopOpacity="0" />
            </RadialGradient>
          </Defs>
          <Rect
            x="0"
            y="0"
            width="100%"
            height="100%"
            fill="url(#grad1)"
            rx="3"
            ry="3"
          />
        </Svg>
      }
      {colors.length > 1 &&
        <Svg height="100%" width="100%" style={StyleSheet.absoluteFill}>
          <Defs>
            <RadialGradient
              id="grad2"
              cx="75%"
              cy="75%"
              r="37%"
              fx="90%"
              fy="90%"
            >
              <Stop offset="0%" stopColor={colors[1]} stopOpacity="0.5" />
              <Stop offset="100%" stopColor={colors[1]} stopOpacity="0" />
            </RadialGradient>
          </Defs>
          <Rect
            x="0"
            y="0"
            width="100%"
            height="100%"
            fill="url(#grad2)"
            rx="3"
            ry="3"
          />
        </Svg>
      }
    {borders &&
      <>
        <Svg style={StyleSheet.absoluteFill}>
          <Defs>
            <LinearGradient id="grad" x1="0%" y1="0%" x2="0.3%" y2="100%">
              <Stop offset="0%" stopColor="#000000" stopOpacity=".2" />
              <Stop offset="100%" stopColor="#000000" stopOpacity="0" />
            </LinearGradient>
          </Defs>
          <Rect
            x="0"
            y="0"
            width="100%"
            height={30}
            fill="url(#grad)"
            rx={3}
            ry={3}
          />
        </Svg>
        <Svg style={StyleSheet.absoluteFill}>
          <Defs>
            <LinearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0.04%">
              <Stop offset="0%" stopColor="#000000" stopOpacity=".2" />
              <Stop offset="100%" stopColor="#000000" stopOpacity="0" />
            </LinearGradient>
          </Defs>
          <Rect
            x="0"
            y="0"
            width={20}
            height="100%"
            fill="url(#grad)"
            rx={3}
            ry={3}
          />
        </Svg>
        <Svg style={StyleSheet.absoluteFill}>
          <Defs>
            <LinearGradient id="grad" x1="100%" y1="100%" x2="99.95%" y2="0%">
              <Stop offset="0%" stopColor="#ffffff" stopOpacity=".8" />
              <Stop offset="100%" stopColor="#ffffff" stopOpacity="0" />
            </LinearGradient>
          </Defs>
          <Rect
            x="0"
            y="100%"
            width="100%"
            height={12}
            fill="url(#grad)"
            rx={3}
            ry={3}
            transform="translate(0, -12)"
          />
        </Svg>
        <Svg style={StyleSheet.absoluteFill}>
          <Defs>
            <LinearGradient id="grad" x1="100%" y1="100%" x2="0%" y2="99.995%">
              <Stop offset="0%" stopColor="#ffffff" stopOpacity=".8" />
              <Stop offset="100%" stopColor="#ffffff" stopOpacity="0" />
            </LinearGradient>
          </Defs>
          <Rect
            x="100%"
            y="0"
            width={8}
            height="100%"
            fill="url(#grad)"
            rx={3}
            ry={3}
            transform="translate(-8, 0)"
          />
        </Svg>
      </>}
      
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  widget: {
    flex: 1,
    borderRadius: 4,
    borderWidth: 1,
    borderColor: Colors.light.borders,
    margin: 20
    //padding: 10
  }
})

/*
<View style={styles.widgetWrapper}>
          
          {/*
          <View style={{ borderRadius: 200, backgroundColor: 'yellow', position: 'absolute', height: 200, width: 200, top: '40%', right: '40%'}}/>
          <View style={{ borderRadius: 200, backgroundColor: 'black', position: 'absolute', height: 200, width: 200, top: '10%', right: '0%'}}/>
          <View style={{ borderRadius: 200, backgroundColor: 'red', position: 'absolute', height: 200, width: 200, top: '60%', right: '0%'}}/>
          <Svg height="100%" width="100%" style={StyleSheet.absoluteFill}>
            <Defs>
            <RadialGradient
              id="grad1"
              cx="40%"
              cy="50%"
              r="100%"
              fx="50%"
              fy="10%"
            >
              <Stop offset="0%" stopColor="red" stopOpacity="0.8" />
              <Stop offset="100%" stopColor="#dddddd" stopOpacity="0" />
            </RadialGradient>
          </Defs>
          <Rect
            x="0"
            y="0"
            width="100%"
            height="100%"
            fill="url(#grad1)"
            rx="4"
            ry="4"
          />
          </Svg>
          <Svg height="100%" width="100%" style={StyleSheet.absoluteFill}>
            <Defs>
            <RadialGradient
              id="grad2"
              cx="50%"
              cy="50%"
              r="75%"
              fx="100%"
              fy="100%"
            >
              <Stop offset="0%" stopColor="yellow" stopOpacity="0.8" />
              <Stop offset="100%" stopColor="#dddddd" stopOpacity="0" />
            </RadialGradient>
          </Defs>
          <Rect
            x="0"
            y="0"
            width="100%"
            height="100%"
            fill="url(#grad2)"
            rx="40"
            ry="40"
          />
          </Svg>
        </View>

          const [orientation, setOrientation] = useState({ alpha: 0, beta: 0, gamma: 0 });

  useEffect(() => {
    const subscription = DeviceMotion.addListener((motion) => {
      if (motion.rotation) {
        setOrientation({
          alpha: motion.rotation.alpha, // z-axis (yaw)
          beta: motion.rotation.beta,   // x-axis (pitch)
          gamma: motion.rotation.gamma, // y-axis (roll)
        });
      }
    });

    return () => subscription.remove();
  }, []);

  function getScreenNormalVector(alpha: number, beta: number, gamma: number) {
  // Rotation matrices
  const cA = Math.cos(alpha);
  const sA = Math.sin(alpha);
  const cB = Math.cos(beta);
  const sB = Math.sin(beta);
  const cG = Math.cos(gamma);
  const sG = Math.sin(gamma);

  // Apply Z (alpha), X (beta), Y (gamma) rotation in order
  // The forward vector of the screen in device coordinates is [0, 0, -1]
  // We rotate that vector using the combined rotation matrix

  const x = -cG * sA - sG * sB * cA;
  const y = -sG * sA + cG * sB * cA;
  const z = cB * cA;

  return { x, y, z };
}

function getInterpolatedColor(value: number, invert: boolean = false) {
  // Clamp between -1.5 and 1.5
  const clamped = Math.max(-1.5, Math.min(1.5, value));

  // Map -1.5 → 0 (black), +1.5 → 1 (white)
  const brightness = invert? 1 - (clamped + 1.5) / 3 : (clamped + 1.5) / 3;  // range: 0 to 1

  const colorValue = Math.round(brightness * 255);
  const hex = colorValue.toString(16).padStart(2, '0');

  return `#${hex}${hex}${hex}`; // grayscale color
}

const screenVector = getScreenNormalVector(orientation.alpha, orientation.beta, orientation.gamma);

,
  widget: {
    borderColor: "white",
    borderWidth: 0.5,
    borderRadius: 4,
    height: "100%",
    width: "100%"
  },
  widgetWrapper: {
    marginHorizontal: 20,
    marginVertical: 60,
    flex: 1,
    overflow: 'hidden',
    backgroundColor: "#dddddd"
  }
*/