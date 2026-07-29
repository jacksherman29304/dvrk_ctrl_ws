import matplotlib.pyplot as plt
import os, time

LOG_DIR = '/home/dvrk-team/internship/logs'


def plot_error(d, r, p, y, tag='lift'):

    iter = range(len(d))


    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 7))

    ax1.plot(iter, r, label='roll')
    ax1.plot(iter, p, label='pitch')
    ax1.plot(iter, y, label='yaw')
    ax1.axhline( 0.01, ls='--', c='k', lw=0.8)
    ax1.axhline(-0.01, ls='--', c='k', lw=0.8, label='rot deadband')
    ax1.set_ylabel('rotational error (rad)')
    ax1.legend(loc='best')
    ax1.grid(alpha=0.3)

    ax2.plot(iter, d, c='tab:purple')
    ax2.axhline(0.005, ls='--', c='k', lw=0.8, label='pos deadband')
    ax2.set_ylabel('dist to target (m)')
    ax2.set_xlabel('iteration')
    ax2.legend(loc='best')
    ax2.grid(alpha=0.3)
    os.makedirs(LOG_DIR, exist_ok=True)
    name = f"{tag}_{time.strftime('%Y%m%d_%H%M%S')}.png"
    out = os.path.join(LOG_DIR, name)

    fig.suptitle(name)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"saved {out}")
    return out