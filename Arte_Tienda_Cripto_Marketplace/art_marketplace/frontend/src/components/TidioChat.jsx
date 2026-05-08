import { useEffect } from 'react';

const TIDIO_PUBLIC_KEY = 'xqk3bz3n2zn3pe3wzuf9vopfebmogxm0';

export default function TidioChat() {
  useEffect(() => {
    if (!TIDIO_PUBLIC_KEY || document.getElementById('tidio-script')) return;

    const script = document.createElement('script');
    script.id = 'tidio-script';
    script.src = `//code.tidio.co/${TIDIO_PUBLIC_KEY}.js`;
    script.async = true;
    document.body.appendChild(script);

    return () => {
      const el = document.getElementById('tidio-script');
      if (el) el.remove();
    };
  }, []);

  return null;
}
