# Authored by:
# Mona Tlili
# Nicklas Kjellbom
# Filip Lindgren Dewari
# Thomas Stabforsmo Norell

import spade

class DummyAgent(spade.agent.Agent):
    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))

async def main():
    dummy = DummyAgent("monatlilijabber.cz@", "jagskainteglommamittlosenord")
    await dummy.start()

if __name__ == "__main__":
    spade.run(main())