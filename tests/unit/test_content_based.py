import pandas as pd

from app.algorithms.content_based import ContentBased


def test_get_similar_movies():
    mock_data = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "title": [
                "Titanic",
                "Avatar",
                "Terminator 3: Rise of the Machines",
                "Terminator",
            ],
            "overview": [
                "84 years later, a 101-year-old woman named Rose DeWitt Bukater tells the story to her granddaughter Lizzy Calvert, Brock Lovett, Lewis Bodine, Bobby Buell and Anatoly Mikailavich on the Keldysh about her life set in April 10th 1912, on a ship called Titanic when young Rose boards the departing ship with the upper-class passengers and her mother, Ruth DeWitt Bukater, and her fiancÃ©, Caledon Hockley. Meanwhile, a drifter and artist named Jack Dawson and his best friend Fabrizio De Rossi win third-class tickets to the ship in a game. And she explains the whole story from departure until the death of Titanic on its first and last voyage April 15th, 1912 at 2:20 in the morning.",
                "In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.",
                "It's been 10 years since John Connor saved Earth from Judgment Day, and he's now living under the radar, steering clear of using anything Skynet can trace. That is, until he encounters T-X, a robotic assassin ordered to finish what T-1000 started. Good thing Connor's former nemesis, the Terminator, is back to aid the now-adult Connor just like he promised.",
                "In the post-apocalyptic future, reigning tyrannical supercomputers teleport a cyborg assassin known as the Terminator back to 1984 to kill Sarah Connor, whose unborn son is destined to lead insurgents against 21st century mechanical hegemony. Meanwhile, the human-resistance movement dispatches a lone warrior to safeguard Sarah. Can he stop the virtually indestructible killing machine?",
            ],
        }
    )

    cb = ContentBased(mock_data)

    recommendations = cb.get_similar_movies(
        title="Terminator", number_of_movies=2
    )

    assert len(recommendations) == 2
    assert "id" in recommendations[0]
    assert recommendations[0]["title"] == "Terminator 3: Rise of the Machines"
    assert (
        recommendations[0]["similarity_score"]
        >= recommendations[1]["similarity_score"]
    )
