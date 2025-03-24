import pygame


class SoundManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SoundManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self._sounds = {}
            self._channels = {}
            self._background_music = None
            pygame.mixer.pre_init()
            pygame.mixer.set_num_channels(64)
            # pygame.mixer.init()
    
    def load_sound(self, name, filepath, 
                   volumne=0.5, 
                   freq=200,
                   channel=0):
        """Loads a sound effect and assigns it a name."""
        self._sounds[name] = {"sound": pygame.mixer.Sound(filepath),
                              "freq": freq,
                              'last_played': 0}
        self._sounds[name]['sound'].set_volume(volumne)
        self._channels[name] = pygame.mixer.Channel(channel)

    def play_sound(self, name):
        """Plays a specific sound effect."""
        if name in self._sounds:
            # if not pygame.mixer.get_busy():
                now = pygame.time.get_ticks()
                freq = self._sounds[name]['freq']
                last_played = self._sounds[name]['last_played']
                if now - last_played > freq: 
                    self._channels[name].play(self._sounds[name]['sound'])
                    self._sounds[name]['last_played'] = now
        else:
            print(f"Sound '{name}' not found!")

    def set_background_music(self, filepath):
        """Loads and sets the background music."""
        self._background_music = filepath
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.set_volume(0.2)  # Adjust the volume

    def play_background_music(self, loops=-1, start=0.0, fade_ms=0):
        """Starts playing the background music."""
        if self._background_music:
            pygame.mixer.music.play(loops=loops, start=start, fade_ms=fade_ms)
        else:
            print("Background music not set!")

    def stop_background_music(self):
        """Stops the background music."""
        pygame.mixer.music.stop()

    def stop_all_sounds(self):
        """Stops all currently playing sounds."""
        pygame.mixer.stop()
